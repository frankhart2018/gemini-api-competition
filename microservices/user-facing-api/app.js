import express from "express";
import cors from "cors";
import connectDB from './config/db.js';
import dotenv from 'dotenv';
import UsersController from './controllers/users/user-controller.js';
import ProfileController from "./controllers/profiles/profile-controller.js";
import QuestionController from "./controllers/questions/question-controller.js";
import UserAnswerController from "./controllers/userAnswers/useranswer-controller.js";
import NotificationController from "./controllers/notifications/notification-controller.js";
// Load config
dotenv.config();


const corsOptions = {
        origin: "*",
        credentials: true, //access-control-allow-credentials:true
        optionSuccessStatus: 200,
    };
    const app = express();
    // Connect Database
    await connectDB();

    app.use(cors(corsOptions));
    app.use(express.json());
  
UsersController(app);
ProfileController(app);
QuestionController(app);
UserAnswerController(app);
NotificationController(app);
app.listen(process.env.PORT || 4000);