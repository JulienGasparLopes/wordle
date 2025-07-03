import { Metadata } from "next"
import { renameAction } from "./actions"

export const metadata: Metadata = {
  title: "Rename",
  description: "Rename your username",
}

const RenamePage = () => {
  return (
    <div className="flex flex-col items-center justify-center h-full">
      <div className="w-96 rounded-lg bg-gray-800 p-8 shadow-lg">
        <h1 className="text-2xl font-bold text-white text-center mb-6">
          Choose a username
        </h1>
        <form className="flex flex-col gap-4">
          <input
            className="bg-gray-700 text-white rounded-md p-3 border border-gray-600 focus:outline-none focus:ring-2 focus:ring-orange-500"
            type="text"
            name="pseudo"
            placeholder="Enter your username"
          />
          <button
            className="bg-blue-600 text-white rounded-md p-3 flex items-center justify-center gap-2 hover:bg-blue-700 transition-colors"
            formAction={renameAction}
          >
            Validate
          </button>
        </form>
      </div>
    </div>
  )
}

export default RenamePage
