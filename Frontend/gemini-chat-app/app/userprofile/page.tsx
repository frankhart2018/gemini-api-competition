import { Separator } from "@/components/ui/separator"
import { ProfileForm } from "./profiile-form"

export default function SettingsProfilePage() {
  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-medium">Profile</h3>
        <p className="text-sm text-muted-foreground">
          Something about the user.
        </p>
      </div>
      <Separator />
      <ProfileForm />
    </div>
  )
}
