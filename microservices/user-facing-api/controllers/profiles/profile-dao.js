import profileModel from "./profile-model.js";
export const findProfile = (userId) => {
  return profileModel.findOne({ userId: userId });
}

export const createProfile = (userId, bio, age, location, interests) => {
  return profileModel.create({ userId, bio, age, location, interests });
}

export const updateProfile = (userId, bio, age, location, interests) => {
  return profileModel.findOneAndUpdate({ userId: userId }, { bio, age, location, interests }, { new: true });
}

export const findRequest=async (userId,friendId)=>{
  const userProfile=await profileModel.findOne({userId:userId});
  const result=await userProfile.friends.find(friend => friend.receiverId.toString() === friendId && friend.status === 'pending');
  return result
}

export const sendRequest=async (userId,friendId)=>{
  const user=await profileModel.findOne({userId:userId});
  const friend=await profileModel.findOne({userId:friendId});
  user.friends.push({receiverId:friendId,status:'pending'});
  friend.friends.push({receiverId:userId,status:'pending'});
  user.save();
  friend.save();
}

export const respondToRequest=async (userId,friendId,status)=>{
    const user=await profileModel.findOne({userId:userId});
    const friend=await profileModel.findOne({userId:friendId});
    const userFriend=user.friends.find(friend => friend.receiverId.toString() === friendId && friend.status === 'pending');
    const friendFriend=friend.friends.find(friend => friend.receiverId.toString() === userId && friend.status === 'pending');
    if(status==='accepted'){
        userFriend.status='accepted';
        friendFriend.status='accepted';
    }   
    if(status==='declined'){
        // remove friend from users's friend list
        user.friends = user.friends.filter(friend => friend.receiverId.toString() !== friendId);
        // remove user from friends's friend list
        friend.friends = friend.friends.filter(friend => friend.receiverId.toString() !== userId);
    }
    user.save();
    friend.save();
}