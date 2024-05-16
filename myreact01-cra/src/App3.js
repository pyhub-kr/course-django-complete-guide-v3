import Avatar from "./components/Avatar";

function App() {
  return (
    <div>
      <Avatar
        name={"django"}
        // image_url={"https://github.com/django.png"}
        image_url={undefined}
        url={"https://github.com/django/django"}
        badge={1}
      />
      <Avatar
        name={"react"}
        // image_url={"https://github.com/facebook.png"}
        image_url={undefined}
        url={"https://github.com/facebook/react"}
        badge={4}
      />
    </div>
  );
}

export default App;
