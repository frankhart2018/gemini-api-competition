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
            await userAnswerDao.createUserAnswer(userId, questionAnsObj);
            return res.status(201).send({ message: "User answer created successfully" });
        }
        await userAnswerDao.updateUserAnswer(userId, questionAnsObj);
        res.send({ message: "User answer updated successfully" });
    } catch (err) {
        res.status(500).send({ message: "An error occurred" });
    }
}

export default UserAnswerController;