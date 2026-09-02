import API from "./api";

export const registerUser = (data) => {
  return API.post("accounts/register/", data);
};

export const loginUser = (data) => {
  return API.post("accounts/login/", data);
};