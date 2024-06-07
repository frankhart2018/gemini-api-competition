import { Separator } from "@/components/ui/separator"
import { ProfileForm } from "./profiile-form"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"


export default function SettingsProfilePage() {
  return (
    <div className="space-y-6">
      <div>
        <Avatar className="w-16 h-16"> {/* Increase the size of the avatar */}
            <AvatarImage  src=" " alt="random picture" />
            <AvatarFallback>CN</AvatarFallback>
        </Avatar>
        <h3 className="text-lg font-medium py-3 px-1">Profile</h3>
        <p className="text-sm text-muted-foreground px-1">
          Something about the user.
        </p>
      </div>
      <Separator />
      <ProfileForm />
    </div>
  )
}
