import { useEffect, useState } from "react";
import Axios from "axios";

// import "bootstrap/dist/css/bootstrap.css";  // bootstrap5 CSS

const DATA_URL = "https://pyhub.kr/melon/20231116.json";

function MelonSongList() {
  const [songList, setSongList] = useState([]);

  async function loadSingList() {
    const _songList = (await Axios.get(DATA_URL)).data;
    setSongList(_songList);
  }

  useEffect(() => {
    loadSingList();
  }, []);

  return (
    <div className="container">
      <h2>멜론 TOP100</h2>

      <div className="my-3">
        <button className="btn btn-primary" onClick={() => loadSingList()}>
          새로고침
        </button>
      </div>

      <table className="table table-bordered table-hover">
        <thead>
          <tr>
            <th>앨범</th>
            <th>곡</th>
            <th>좋아요</th>
          </tr>
        </thead>
        <tbody>
          {songList.map((song) => (
            <tr key={song.곡일련번호}>
              <td>
                <img
                  src={song.커버이미지_주소}
                  className="rounded"
                  style={{ width: "2em" }}
                />
              </td>
              <td>
                {song.곡명}
                <small className="text-sm-start"> - {song.가수}</small>
              </td>
              <td className="text-end">{song.좋아요}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default MelonSongList;
