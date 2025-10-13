"use client";

import { useState } from "react";
import PropTypes from "prop-types";
import { useNavigate, Link } from "react-router-dom";
import { Eye, EyeOff, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import api from "../api";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";

function Form({ route, method }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  const isLogin = method === "login";
  const title = isLogin ? "Welcome Back" : "Create an Account";
  const buttonText = isLogin ? "Sign In" : "Sign Up";

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (!username.trim() || !password.trim()) {
      setError("Username and password are required");
      return;
    }

    setLoading(true);

    try {
      const res = await api.post(route, { username, password });
      if (isLogin) {
        localStorage.setItem(ACCESS_TOKEN, res.data.access);
        localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
        navigate("/");
      } else {
        navigate("/login");
      }
    } catch (err) {
      const errorMessage =
        err.response?.data?.detail ||
        err.response?.data?.message ||
        "An error occurred. Please try again.";
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex justify-center items-center min-h-[80vh] px-4">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1">
          <CardTitle className="text-2xl font-bold text-center">
            {title}
          </CardTitle>
          <CardDescription className="text-center">
            Enter your credentials to {isLogin ? "sign in to" : "create"} your
            account
          </CardDescription>
        </CardHeader>
        <CardContent>
          {error && (
            <Alert variant="destructive" className="mb-4">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="username">Username</Label>
              <Input
                id="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Enter your username"
                disabled={loading}
                className="h-11"
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <div className="relative">
                <Input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter your password"
                  disabled={loading}
                  className="h-11 pr-10"
                />
                <Button
                  type="button"
                  variant="ghost"
                  size="icon"
                  className="absolute right-0 top-0 h-11 w-11"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? (
                    <EyeOff className="h-4 w-4" />
                  ) : (
                    <Eye className="h-4 w-4" />
                  )}
                  <span className="sr-only">
                    {showPassword ? "Hide password" : "Show password"}
                  </span>
                </Button>
              </div>
            </div>
            <Button
              type="submit"
              className="w-full h-11 mt-6"
              disabled={loading}
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Please wait
                </>
              ) : (
                buttonText
              )}
            </Button>
          </form>
        </CardContent>
        {isLogin && (
          <CardFooter className="flex flex-col">
            <div className="text-center text-sm mt-2">
              Don&apos;t have an account?{" "}
              <Link
                to="/register"
                className="underline text-primary hover:text-primary/90 font-medium"
              >
                Create account
              </Link>
            </div>
          </CardFooter>
        )}
      </Card>
    </div>
  );
}

Form.propTypes = {
  route: PropTypes.string.isRequired,
  method: PropTypes.string.isRequired,
};

export default Form;
