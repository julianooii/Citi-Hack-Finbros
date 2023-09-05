import "./RequestAcc.css";
import { Link, useNavigate } from "react-router-dom";

const RequestAcc = () => {
    return(
        <div className="modal">
        <form>
        <input
          className="modal-field"
          type="number"
          placeholder="Employee ID"
        //   onChange={(e) => setEmail(e.target.value)}
        />
        <input
          className="modal-field"
          type="text"
          placeholder="Department"
        //   onChange={(e) => setPassword(e.target.value)}
        />
        <button className="button" type="submit">
          Request
        </button>
      </form>
      </div>
    );
};

export default RequestAcc;