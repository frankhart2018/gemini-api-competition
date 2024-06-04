import userAnswerModel from "./useranswer-model.js";

export const findUser = (userId) => {
    return userAnswerModel.findOne({ user_id: userId });
    };

export const createUserAnswer = (userId, questionAnsObj) => {

    userAnswerModel.create({ user_id: userId, questionAnsObj });

    }
export const updateUserAnswer = (userId, questionAnsObj) => {
    return userAnswerModel.findOneAndUpdate({ user_id: userId }, { questionAnsObj }, { new: true });
}