import { Link, useNavigate } from "react-router-dom";
import "./SignIn.css";

const SignIn = () => {
    return (
        <div className="modal">
      <div className="logo">
        
      </div>
      <form>
        <input
          className="modal-field"
          type="number"
          placeholder="Employee ID"
        //   onChange={(e) => setEmail(e.target.value)}
        />
        <input
          className="modal-field"
          type="password"
          placeholder="Password"
        //   onChange={(e) => setPassword(e.target.value)}
        />
        <p>
          Don't have an account?<br></br><br></br>
          <Link className="sign-up-link" to="/requestacc">
            Request for an account
          </Link>
        </p>
        <button className="button" type="submit" to = "/">
          Sign In
        </button>
      </form>
    </div>
    )
}
export default SignIn;