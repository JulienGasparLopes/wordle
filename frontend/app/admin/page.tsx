import Link from "next/link";

export default async function Game({ params }: any) {
  return (
    <div className="flex flex-col gap-4">
      <Link href="/admin/game/new">Create Game</Link>
      <Link href="/admin/migrate/user">Migrate User Account</Link>
      <Link href="/admin/migrate/game">Migrate Games</Link>
    </div>
  );
}
