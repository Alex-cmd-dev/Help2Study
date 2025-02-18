import Form from "../components/Form";

function Register() {
  return (
    <div className="flex justify-center items-center min-h-screen">
      <Form
        className="w-full max-w-md"
        route="/api/user/register/"
        method="register"
      />
    </div>
  );
}

export default Register;
