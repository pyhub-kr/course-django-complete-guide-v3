import "./Avatar.css";
import PropTypes from "prop-types";

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

Avatar.propTypes = {
  name: PropTypes.string,
  image_url: PropTypes.string.isRequired,
  url: PropTypes.string,
  badge: PropTypes.number,
};

export default Avatar;
