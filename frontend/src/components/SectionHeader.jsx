function SectionHeader({
  title,
  description,
}) {
  return (
    <div className="mb-6">
      <div className="mb-2 flex items-center gap-3">

        <h3 className="text-lg font-semibold">
          {title}
        </h3>
      </div>

      <p className="text-sm text-gray-500">
        {description}
      </p>
    </div>
  );
}

export default SectionHeader;