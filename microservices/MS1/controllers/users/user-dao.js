import userModel from "./user-model.js";

export const findUser = (email) => {
  return userModel.findOne({ email: email });
};


export const createUser = (email, password, username) => {
    return userModel.create({ email, password, username });
    }

export const findUserById = (id) => {
  return userModel.findOne({ _id: id });
};

export const updatePassword = (id, password) => {
    return userModel.updateOne({ _id: id }, { password: password });
  };