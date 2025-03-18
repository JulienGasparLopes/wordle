import { loginAction } from "./actions";

const Login = () => {
  return (
    <div className="h-full p-8 flex flex-col w-64 justify-center items-center m-auto">
      <h1>Select a pseudo</h1>
      <form>
        <input className="text-black" type="text" name="pseudo" />
        <button formAction={loginAction}>Login</button>
      </form>
    </div>
  );
};

export default Login;
