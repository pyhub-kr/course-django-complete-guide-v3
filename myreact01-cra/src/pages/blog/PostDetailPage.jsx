import { NavLink, useParams } from "react-router-dom";
import { postList } from "./data";
import { Alert } from "react-bootstrap";

function PostDetailPage() {
  const { postId } = useParams();

  const numberPostId = parseInt(postId, 10);

  /* 아직은 API를 호출하지 않고 더미 데이터를 조회합니다. */
  const post = postList.find((post) => post.id === numberPostId);

  if (!post) {
    return <Alert variant="danger">글을 찾을 수 없습니다.</Alert>;
  }

  return (
    <div>
      <h3>{post.title}</h3>
      <div>{post.content}</div>
      <hr />
      <NavLink to="/blog">목록으로</NavLink>
    </div>
  );
}

export default PostDetailPage;
