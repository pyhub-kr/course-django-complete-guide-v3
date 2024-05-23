# core/management/commands/react-components.py
import glob
import json
import os
import re
import shutil
import subprocess
import threading
import time
import webbrowser
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from django.conf import settings
from django.core.management import BaseCommand, CommandError, call_command
from django.template import Template, Context
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from watchdog.observers import Observer

# refs: https://parceljs.org/features/cli/
COMMANDS = {
    # HMR 포트를 지정했지만 반영되지 않음
    "start": "parcel --dist-dir ../src-django-components/react_dist --public-url /static/react_dist --hmr-host 127.0.0.1 --hmr-port 1234",
    # HMR 옵션 없이도 127.0.0.1:1234 주소로 HMR 접속
    "watch": "parcel watch ./src/*.html --no-cache --dist-dir ../src-django-components/react_dist --public-url /static/react_dist",
    "build": "parcel build ./src/*.html --no-cache --no-scope-hoist --no-source-maps --dist-dir ../src-django-components/react_dist --public-url /static/react_dist",
}

REACT_COMPONENTS_PATH = settings.BASE_DIR / "core" / "src-react-components"
DJANGO_COMPONENTS_PATH = settings.BASE_DIR / "core" / "src-django-components"
REACT_DIST_PATH = DJANGO_COMPONENTS_PATH / "react_dist"
REACT_MAP_PATH = settings.BASE_DIR / "core" / "react_components_map.py"

INITIAL_PACKAGE_NAMES = "react@18 react-dom@18"
INITIAL_DEV_PACKAGE_NAMES = "parcel@2"


GIST_ID = "87dab7c2d7c1d1efa6360b835d54c83f"
GIST_API_URL = f"https://api.github.com/gists/{GIST_ID}"


class Command(BaseCommand):
    def add_arguments(self, parser):
        subparsers = parser.add_subparsers(dest="sub_command")

        subparsers.add_parser("init", help="react 컴포넌트 프로젝트를 초기화합니다.")

        subparsers.add_parser("view", help="gist에 업로드된 코드를 확인합니다.")

        subparsers.add_parser(
            "add-commands", help="npm 명령어를 package.json에 추가합니다."
        )

        parser_install = subparsers.add_parser(
            "install", help="npm 패키지를 설치합니다."
        )
        parser_install.add_argument(
            "package_names", nargs="*", type=str, help="설치할 팩키지명을 지정합니다."
        )
        parser_install.add_argument(
            "--dev-package-names",
            nargs="*",
            type=str,
            help="설치할 개발용 팩키지명을 지정합니다.",
        )

        parser_create = subparsers.add_parser(
            "create", help="새로운 리액트 컴포넌트를 생성합니다."
        )
        parser_create.add_argument(
            "component_name", type=str, help="생성할 컴포넌트명을 지정합니다."
        )
        parser_create.add_argument(
            "--no-py",
            action="store_true",
            help="장고 템플릿 컴포넌트도 같이 생성합니다.",
        )

        subparsers.add_parser("clean", help="빌드된 컴포넌트를 삭제합니다.")

        parser_start = subparsers.add_parser(
            "start", help="지정 entry의 컴포넌트를 실행합니다."
        )
        parser_start.add_argument(
            "entry",
            type=str,
            help="컴포넌트의 진입점인 html 파일 경로를 지정합니다.",
        )

        subparsers.add_parser("watch", help="컴포넌트를 변경 감지하고 빌드합니다.")
        subparsers.add_parser("build", help="컴포넌트를 빌드합니다.")

        parser_build_map = subparsers.add_parser(
            "build-map", help="빌드된 컴포넌트의 파이썬 매핑 파일을 생성합니다."
        )
        parser_build_map.add_argument(
            "--once", action="store_true", help="한 번만 실행합니다."
        )

    def handle(self, *args, sub_command, **options):
        gist_obj = requests.get(GIST_API_URL).json()

        if sub_command == "view":
            url = f"https://gist.github.com/allieus/{GIST_ID}"
            webbrowser.open_new(url)
        elif sub_command == "init":
            REACT_COMPONENTS_PATH.mkdir(parents=True, exist_ok=True)

            base_js_code = gist_obj["files"]["base.js"]["content"]

            base_js_path = REACT_COMPONENTS_PATH / "src" / "base.js"
            base_js_path.parent.mkdir(parents=True, exist_ok=True)
            base_js_path.open("wt", encoding="utf-8").write(base_js_code)
            print("base.js 파일을 생성했습니다.")

            print("팩키지 설치 중 ...")
            call_command(
                "react-components",
                f"install {INITIAL_PACKAGE_NAMES} --dev-package-names {INITIAL_DEV_PACKAGE_NAMES}".split(),
            )
            call_command("react-components", "add-commands".split())
        elif sub_command == "add-commands":
            package_json_path = REACT_COMPONENTS_PATH / "package.json"
            json_string = package_json_path.open("rt", encoding="utf-8").read()
            obj = json.loads(json_string)
            obj["scripts"] = COMMANDS
            json_string = json.dumps(obj, indent=2)
            package_json_path.open("wt", encoding="utf-8").write(json_string)
            self.stdout.write("package.json 파일에 명령어를 추가했습니다.")
        elif sub_command == "install":
            package_names = " ".join(options["package_names"])
            dev_package_names = " ".join(options.get("dev_package_names") or [])
            os.chdir(REACT_COMPONENTS_PATH)
            os.system(f"npm install {package_names}")
            if dev_package_names:
                os.system(f"npm install --save-dev {dev_package_names}")
        elif sub_command == "create":
            is_create_dj_component: bool = options["no_py"] is False

            component_name = options["component_name"]
            component_name = "-".join(
                re.findall(r"([a-zA-Z][a-zA-Z\d]+)", component_name)
            )
            print(f"생성할 컴포넌트 명: {component_name}")

            kebab_name = component_name
            snake_name = kebab_name.replace("-", "_")
            camel_name = "".join([word.capitalize() for word in kebab_name.split("-")])
            context = Context(
                {
                    "kebab_name": kebab_name,
                    "snake_name": snake_name,
                    "camel_name": camel_name,
                }
            )

            src_path = REACT_COMPONENTS_PATH / "src"
            src_path.mkdir(parents=True, exist_ok=True)

            html_path = src_path / (snake_name + ".html")
            if html_path.exists():
                raise CommandError(f"{html_path} 파일이 이미 존재합니다.")

            html_tpl = Template(gist_obj["files"]["snake_name.html-tpl"]["content"])
            html_path.open("wt", encoding="utf-8").write(html_tpl.render(context))
            print(f"created to {html_path}")

            js_tpl = Template(gist_obj["files"]["snake_name.js-tpl"]["content"])
            js_path = src_path / (snake_name + ".js")
            js_path.open("wt", encoding="utf-8").write(js_tpl.render(context))
            print(f"created to {js_path}")

            css_module_tpl = Template(
                gist_obj["files"]["snake_name.module.css-tpl"]["content"]
            )
            css_module_path = src_path / (snake_name + ".module.css")
            css_module_path.open("wt", encoding="utf-8").write(
                css_module_tpl.render(context)
            )
            print(f"created to {css_module_path}")

            if is_create_dj_component:
                django_component_py_tpl = Template(
                    gist_obj["files"]["snake_name.django.py-tpl"]["content"]
                )
                django_component_py_path = (
                    DJANGO_COMPONENTS_PATH / snake_name / (snake_name + ".py")
                )
                django_component_py_path.parent.mkdir(parents=True, exist_ok=True)
                django_component_py_path.open("wt", encoding="utf-8").write(
                    django_component_py_tpl.render(context)
                )
                print(f"created to {django_component_py_path}")

                django_component_html_tpl = Template(
                    gist_obj["files"]["snake_name.django.html-tpl"]["content"]
                )
                django_component_html_path = (
                    DJANGO_COMPONENTS_PATH / snake_name / (snake_name + ".html")
                )
                django_component_html_path.parent.mkdir(parents=True, exist_ok=True)
                django_component_html_path.open("wt", encoding="utf-8").write(
                    django_component_html_tpl.render(context)
                )
                print(f"created to {django_component_html_path}")
        elif sub_command == "clean":
            shutil.rmtree(DJANGO_COMPONENTS_PATH / "react_dist", ignore_errors=True)
            REACT_MAP_PATH.open("wt", encoding="utf-8").write("mapper = {}\n")

        elif sub_command in ("start", "watch"):
            process_npm = None
            process_build_map = None

            if sub_command == "start":
                entry_path = options["entry"]
                if not entry_path.endswith(".html"):
                    raise CommandError("entry는 html 파일이어야 합니다.")
                npm_cmd = f"npm run start src/{entry_path}"
                build_map_cmd = "python manage.py react-components build-map --once"
            else:  # watch
                npm_cmd = "npm run watch"
                build_map_cmd = "python manage.py react-components build-map"

            os.chdir(REACT_COMPONENTS_PATH)
            try:
                process_npm = subprocess.Popen(npm_cmd.split())

                os.chdir(settings.BASE_DIR)
                process_build_map = subprocess.Popen(build_map_cmd.split())
                print("Enter Ctrl-C to stop")

                while True:
                    time.sleep(0.1)
            except (KeyboardInterrupt, EOFError):
                if process_npm is not None:
                    print("terminate process_npm ...")
                    process_npm.terminate()
                if process_build_map is not None:
                    print("terminate process_build_map ...")
                    process_build_map.terminate()

        elif sub_command == "build":
            os.chdir(REACT_COMPONENTS_PATH)
            os.system("npm run build")

            os.chdir(settings.BASE_DIR)
            os.system("python manage.py react-components build-map --once")

        elif sub_command == "build-map":
            is_once: bool = options["once"]
            watch_handler = WatchHandler(REACT_DIST_PATH, REACT_MAP_PATH)
            if is_once is False:
                observer = Observer()
                observer.schedule(watch_handler, REACT_DIST_PATH, recursive=True)
                observer.start()

                try:
                    while True:
                        time.sleep(0.1)
                except (KeyboardInterrupt, EOFError):
                    observer.stop()
                    observer.join()

                print("End of watch")

        else:
            raise CommandError(f"{sub_command} 명령은 지원하지 않는 명령입니다.")


def remove_files_with_glob(file_pattern: str) -> None:
    for name in glob.glob(file_pattern):
        os.unlink(name)
        print("removed", name)


class WatchHandler(FileSystemEventHandler):
    def __init__(self, dist_path: Path, map_path: Path):
        self.dist_path = dist_path
        self.map_path = map_path

        self.debounce_timer = None
        self.debounce_interval = 0.1
        self.task()

    def on_any_event(self, event: FileSystemEvent) -> None:
        # 기존 타이머가 있으면 취소
        if self.debounce_timer is not None:
            self.debounce_timer.cancel()

        # 새로운 타이머 시작
        self.debounce_timer = threading.Timer(self.debounce_interval, self.task)
        self.debounce_timer.start()

    def task(self) -> None:
        dist_dir_name = self.dist_path.name
        pattern = rf"^.*?(?={dist_dir_name}/)"

        mapper = {}
        for html_path in self.dist_path.glob("*.html"):
            html: str = html_path.open("rt", encoding="utf-8").read()
            soup = BeautifulSoup(html, "html.parser")

            css_path_list, js_path_list = [], []

            for tag in soup.select("link, script"):
                if tag.name == "link" and tag.has_attr("href"):
                    if not tag["href"].startswith(("http://", "https://")):
                        css_path = re.sub(pattern, "", tag["href"])
                        css_path_list.append(css_path)
                elif tag.name == "script" and tag.has_attr("src"):
                    if not tag["src"].startswith(("http://", "https://")):
                        js_path = re.sub(pattern, "", tag["src"])
                        js_path_list.append(js_path)

            html_name = html_path.name
            mapper[html_name] = {
                "css": css_path_list,
                "js": js_path_list,
            }

        with self.map_path.open("wt", encoding="utf-8") as f:
            print(
                "# react-components 명령을 통해 자동 생성되는 파일입니다.",
                file=f,
                end="\n",
            )
            print("mapper = ", file=f, end="")
            json.dump(mapper, f, indent=4)

        print("updated to", self.map_path)
