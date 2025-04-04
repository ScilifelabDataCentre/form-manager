import pluginVue from 'eslint-plugin-vue';
import globals from 'globals';
import prettierConfig from 'eslint-config-prettier';


export default [
  {
    files: ['**/*.js', '**/*.vue'],
    ignores: [
      '**/dist',
      '**/src-capacitor',
      '**/src-cordova',
      '**/.quasar',
      '**/node_modules',
      '.eslintrc.js',
    ],

    languageOptions: {
      sourceType: 'module',
      ecmaVersion: 'latest',  // Allows for the parsing of modern ECMAScript features

      globals: {
        ga: 'readonly',  // Google Analytics
        cordova: 'readonly',
        __statics: 'readonly',
        __QUASAR_SSR__: 'readonly',
        __QUASAR_SSR_SERVER__: 'readonly',
        __QUASAR_SSR_CLIENT__: 'readonly',
        __QUASAR_SSR_PWA__: 'readonly',
        process: 'readonly',
        Capacitor: 'readonly',
        chrome: 'readonly',
        ...globals.browser  // https://eslint.vuejs.org/user-guide/
      },
    },

    plugins: {
      // https://eslint.vuejs.org/user-guide/#why-doesn-t-it-work-on-vue-files
      // required to lint *.vue files
      pluginVue,

      // https://github.com/typescript-eslint/typescript-eslint/issues/389#issuecomment-509292674
      // Prettier has not been included as plugin to avoid performance impact
      // add it as an extension for your IDE
    },

    // Add your custom rules here
    rules: {
      'prefer-promise-reject-errors': 'off',

      // allow debugger during development only
      'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    },

    linterOptions: {
      reportUnusedDisableDirectives: true,
    },

    settings: {
      'vue/compiler-macros': true,
    },
  },

  // Include Vue recommended rules
  ...pluginVue.configs['flat/recommended'],

  // Include Prettier configuration
  prettierConfig,
];
