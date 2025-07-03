import { getUserInformation, migrateUser } from "./actions"

export default async function UserMigration() {
  const userInformation = await getUserInformation()

  return (
    <form>
      <div className="flex gap-16">
        <div>
          New Users
          <select name="new_user_id">
            <option value="">Select a user</option>
            {userInformation?.new_users.map((element: any) => {
              return (
                <option key={element.id} value={element.id}>
                  {element.pseudo} - {element.id}
                </option>
              )
            })}
          </select>
        </div>
        <div>
          Old Users
          <select name="old_user_id">
            <option value="">Select a user</option>
            {userInformation?.old_users.map((element: any) => {
              return (
                <option key={element.id} value={element.id}>
                  {element.pseudo} - {element.id}
                </option>
              )
            })}
          </select>
        </div>
      </div>
      <button formAction={migrateUser}>Migrate User</button>
    </form>
  )
}
