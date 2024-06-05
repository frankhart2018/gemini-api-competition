import * as userAnswerDao from "./useranswer-dao.js";


const UserAnswerController = (app) => {
    app.post("/api/questions/answers", createUpdateUserAnswer);
}

const createUpdateUserAnswer = async (req, res) => {
    try {
        const { userId, questionAnsObj} = req.body;
        if (!userId) {
            return res.status(400).send({ message: "User ID is required" });
        }
        if (!Array.isArray(questionAnsObj) || !questionAnsObj.every(obj => obj.hasOwnProperty('question_id') && obj.hasOwnProperty('answer'))) {
            return res.status(400).send({ message: "questionAnsObj must be an array of objects with question_id and answer properties" });
        }
        //insert user_id or update if already exists
        const userPresent = await userAnswerDao.findUser(userId);
        if(!userPresent){
           // user not present return 404
           return res.status(404).send({ message: "User not found" });
        }
        await userAnswerDao.createOrUpdateUserAnswer(userId, questionAnsObj);
        res.send({ message: "User info added successfully" });
    } catch (err) {
        res.status(500).send({ message: "An error occurred" });
    }
}

export default UserAnswerController;