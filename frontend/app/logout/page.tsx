"use client";

import { redirect } from "next/navigation";
import { useEffect } from "react";
import { logoutAction } from "./actions";

const Logout = () => {
  useEffect(() => {
    logoutAction();
  }, []);

  return <div>Logging out...</div>;
};

export default Logout;
