import Form from "../components/Form";

function Login() {
  return (
    <div
      className="flex justify-center items-center min-h-screen"
      data-theme="synthwave"
    >
      <Form route="/api/token/" method="login" className="w-full max-w-md" />
    </div>
  );
}

export default Login;
