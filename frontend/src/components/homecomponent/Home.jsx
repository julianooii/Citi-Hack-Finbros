import "./Home.css";
import { NavLink, useNavigate } from "react-router-dom";
import coverImage from "../../image/cover.png";

const Home = () => {
    return (
        <div className='home'>
            <img className='image' src={coverImage}></img>
        </div>
    )
}
export default Home;