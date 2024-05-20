import useAxios from "axios-hooks";
import { useState } from "react";

const SEARCH_URL = "https://pyhub.kr/melon/search";
const DATA_URL = "https://pyhub.kr/melon/20231116.json";

function MelonSongSearch() {
  const [query, setQuery] = useState("");
  const [{ data: searchResult = [], loading, error }, search] = useAxios(
    SEARCH_URL,
    {
      manual: true,
    },
  );

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      console.log("엔터키가 입력되었습니다. 검색을 수행합니다.");
      const params = { query };
      console.log("검색 요청 파라미터 :", params);
      search({ params });
    }
  };

  return (
    <div className="container">
      <div className="my-3">
        <input
          type="text"
          className="form-control"
          placeholder="검색어를 입력해주세요."
          value={query}
          onChange={(e) => setQuery(e.target.value.trim())}
          onKeyDown={(e) => handleKeyDown(e)}
        />
        {loading && <div className="alert alert-info my-3">로딩 중 ...</div>}
        {searchResult?.SONGCONTENTS && (
          <MelonSongList songList={searchResult.SONGCONTENTS} />
        )}
      </div>
    </div>
  );
}

function MelonSongList({ songList }) {
  return (
    <div className="container">
      <h2>노래 검색결과</h2>

      <table className="table table-bordered table-hover">
        <tbody>
          {songList.map((song) => (
            <tr key={song.SONGID}>
              <td>
                <img
                  src={song.ALBUMIMG}
                  className="rounded"
                  style={{ width: "2em" }}
                />
              </td>
              <td>
                {song.SONGNAME}
                <small className="text-sm-start"> - {song.ARTISTNAME}</small>
              </td>
              <td className="text-end">
                <a
                  href={`https://www.melon.com/song/detail.htm?songId=${song.SONGID}`}
                  target="_blank"
                  rel="noreferrer noopener"
                >
                  노래 바로가기
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default MelonSongSearch;
