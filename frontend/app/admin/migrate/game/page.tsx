import { migrateGames } from "./actions";

export default async function UserMigration({ params }: any) {
  return (
    <form action={migrateGames} className="flex flex-col gap-4">
      <button>Migrate Games</button>
    </form>
  );
}
