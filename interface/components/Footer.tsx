export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-white py-4 text-sm text-gray-500 shadow-inner mt-auto">
      <div className="container mx-auto flex items-center justify-between px-6">
        <span>CEFER USP &copy; {currentYear}</span>
      </div>
    </footer>
  );
}
