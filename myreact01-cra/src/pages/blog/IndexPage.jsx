import { postList } from "./data";
import { NavLink } from "react-router-dom";

function IndexPage() {
  return (
    <div>
      <ul>
        {/* 아직은 API를 호출하지 않고 더미 데이터를 조회합니다. */}
        {postList.map((post) => (
          <li key={post.id}>
            <NavLink to={`/blog/${post.id}`}>{post.title}</NavLink>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default IndexPage;
