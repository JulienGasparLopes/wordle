"use client"

export const LetterInput = ({
  letter,
  focused,
  disabled,
}: {
  letter: string
  focused: boolean
  disabled: boolean
}) => {
  const borderClass = disabled
    ? "border-gray-400"
    : focused
      ? "border-cyan-500 border-2"
      : "border-white border-2"
  const color = disabled ? "bg-gray-400" : "bg-white"
  return (
    <div
      className={`text-black rounded-sm w-10 h-10 ${color} leading-4 justify-items-center justify-center ${borderClass} flex items-center select-none`}
    >
      <p className="text-xl">{letter}</p>
    </div>
  )
}
