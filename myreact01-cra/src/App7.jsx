import useAxios from "axios-hooks";

const DATA_URL = "https://pyhub.kr/melon/20231116.json";

function MelonSongList() {
  const [{ data: songList = [], loading, error }, refetch] = useAxios(DATA_URL);

  // const [songList, setSongList] = useState([]);
  //
  // async function loadSingList() {
  //   const _songList = (await Axios.get(DATA_URL)).data;
  //   setSongList(_songList);
  // }
  //
  // useEffect(() => {
  //   loadSingList();
  // }, []);

  return (
    <div className="container">
      <h2>멜론 TOP100</h2>

      <div className="my-3">
        <button
          className="btn btn-primary"
          onClick={() => refetch()}
          disabled={loading}
        >
          {loading && (
            <span className="spinner-border spinner-border-sm me-1"></span>
          )}
          {!loading && "새로고침"}
        </button>
      </div>

      {error && <div className="alert alert-danger">에러: {error.message}</div>}

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
