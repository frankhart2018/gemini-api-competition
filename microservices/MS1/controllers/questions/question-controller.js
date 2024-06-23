import questions from './questions.js';
import mongoose from 'mongoose';
import * as questionDao from './question-dao.js';
import {logger, LogLevel} from "../../utils/logging.js";
const QuestionController=async (app)=>{
    await insertQuestions();
    app.get("/api/fetchAll",getQuestions);
   
}

const insertQuestions = async () => {
    try {
        const collections = await mongoose.connection.db.listCollections({ name: 'questions' }).toArray();
      if (collections.length === 0) {
        // The collection does not exist, insert the questions
        await questionDao.insertQuestions(questions);
        console.log('Questions added successfully!');
      } else {
        console.log('Questions collection already exists.');
      }
    } catch (err) {
      logger.log(LogLevel.ERROR, err);
      console.error('Error inserting questions:', error);
    }
  };

const getQuestions = async (req, res) => {
    try {
        const questions = await questionDao.getAllQuestions();
        res.send(questions);
    } catch (err) {
        logger.log(LogLevel.ERROR, err);
        res.status(500).send({ message: "An error occurred" });
    }
}

export default QuestionController;