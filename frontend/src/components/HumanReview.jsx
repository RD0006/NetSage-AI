function HumanReview() {
  return (
    <div className="mt-6 rounded-xl border border-amber-400/20 bg-amber-400/5 p-4">
      <p className="text-xs font-medium text-amber-300">
        HUMAN REVIEW
      </p>

      <p className="mt-1 text-xs leading-5 text-gray-500">
        AI recommendations must be reviewed and accepted
        by a human before applying any fix.
      </p>
    </div>
  );
}

export default HumanReview;