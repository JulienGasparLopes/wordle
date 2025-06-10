import { getUserInformation } from "./actions";

export default async function UserMigration({ params }: any) {
  const userInformation = await getUserInformation();
  console.log(userInformation);
  return (
    <div>
      <div>
        New Users
        {userInformation?.new_users.map((element: any) => {
          return (
            <div key={element.id}>
              <p>
                {element.pseudo} - {element.id}
              </p>
            </div>
          );
        })}
      </div>
      <div>
        Old Users
        {userInformation?.old_users.map((element: any) => {
          return (
            <div key={element.id}>
              <p>
                {element.pseudo} - {element.id}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
