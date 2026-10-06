const plans = [
  { id: "starter", name: "Starter", price: "$9/mo" },
  { id: "pro", name: "Pro", price: "$29/mo" },
];

export default function Pricing() {
  return (
    <main>
      {plans.map((plan) => (
        <section key={plan.id}>
          <h2>{plan.name}</h2>
          <p>{plan.price}</p>
          <button disabled>Choose {plan.name}</button>
        </section>
      ))}
    </main>
  );
}
