export { routerAgent, runRouterOnce } from './neuro-seller/router.js';

if (import.meta.url === `file://${process.argv[1]}`) {
  const { runRouterOnce } = await import('./neuro-seller/router.js');
  const result = await runRouterOnce(
    process.argv.slice(2).join(' ') ||
      'Здравствуйте, получил ваше письмо и хотел бы уточнить детали.',
  );
  console.log(result.response);
}
