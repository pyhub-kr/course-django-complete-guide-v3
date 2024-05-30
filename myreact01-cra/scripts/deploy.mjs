// scripts/deploy.mjs

import {execSync} from "child_process";

// 명령행 인자 추출하기
const args = process.argv.slice(2);

const SSH_HOST = args[0];

if (!SSH_HOST) {
  console.error(`Usage: npm run deploy <SSH_HOST>`)
  process.exit(1);
}


const runCommand = (command) => {
  try {
    console.log(`Running command: ${command}`);
    execSync(command, {stdio: "inherit"});
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
};

// 변수 설정
// const SSH_HOST = "django-instance";
const DATETIME = new Date().toISOString().replace(/[-:.]/g, "").slice(0, 15);
const BUILD_PATH = "./build";
const REMOTE_BASE = "/srv/cra-build";
const REMOTE_PATH = `${REMOTE_BASE}/${DATETIME}`;
const LINK_PATH = "/srv/cra-build/current";

// 원격 서버에 디렉토리 생성 및 심볼릭 링크 생성
runCommand(
  `ssh ${SSH_HOST} "mkdir -p ${REMOTE_BASE} && ln -sfn ${REMOTE_PATH} ${LINK_PATH}"`,
);

// 로컬 디렉토리를 원격 서버의 생성된 디렉토리로 복사
runCommand(`scp -r ${BUILD_PATH} ${SSH_HOST}:${REMOTE_PATH}`);
