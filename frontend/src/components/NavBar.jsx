function NavBar() {
  return (
    <div
      className="navbar bg-base-100 shadow-sm absolute top-0 left-1/2 transform -translate-x-1/2"
      data-theme="dracula"
    >
      <div className="flex-1">
        <a className="btn  text-2xl  text-slate-200 ">Help2Study</a>
      </div>
      <div className="  flex-none">
        <ul className="menu menu-horizontal px-1">
          <li>
            <button className="btn btn-soft btn-primary text-slate-200">
              Flashcards
            </button>
          </li>
          <li>
            <button className="btn btn-soft btn-primary text-slate-200">
              Logout
            </button>
          </li>
        </ul>
      </div>
    </div>
  );
}

export default NavBar;
