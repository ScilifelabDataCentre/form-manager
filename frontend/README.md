# Form Manager - frontend

A system for handling form submissions.

## Install the dependencies

```bash
pnpm install
```

## Update the dependencies

Updates packages to their latest version based on the range specified in `package.json`.

```bash
pnpm update
```

Update the dependencies to their latest stable version as determined by their latest tags (potentially upgrading the packages across major versions).

```bash
pnpm update --latest
```

## Start the app in development mode (hot-code reloading, error reporting, etc.)

```bash
quasar dev
```

If quasar CLI is missing:

```bash
pnpm add -g @quasar/cli
```

## Lint the files

```bash
pnpm run lint
```

## Format the files

```bash
pnpm run format
```

## Build the app for production

```bash
quasar build
```

## Customise the configuration

See [Configuring quasar.config.js](https://v2.quasar.dev/quasar-cli-vite/quasar-config-js).
