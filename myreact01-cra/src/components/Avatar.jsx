import "./Avatar.css";

function Avatar({ name, image_url, url, badge }) {
  return (
    <div className="avatar-container">
      <a href={url}>
        <img src={image_url} alt={name} className="avatar-image" />
      </a>
      {badge > 0 && <span className="badge">{badge}</span>}
    </div>
  );
}

export default Avatar;
