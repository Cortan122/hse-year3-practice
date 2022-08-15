<template>
  <div class="min-h-screen flex flex-col sm:justify-center items-center pt-6 sm:pt-0 bg-gray-100">
    <div>
      <router-link to="/">
        <img class="block h-9 w-auto" src="@/assets/logo.png">
      </router-link>
    </div>

    <div class="w-full sm:max-w-md mt-6 px-6 py-4 bg-white shadow-md overflow-hidden sm:rounded-lg">
      <div v-if="error" class="mb-4 font-medium text-red-600">
        Неверное имя пользователя или пароль. Пожалуйста, попробуйте еще раз.
      </div>

      <form action="/api/login" method="POST">
        <div>
          <label class="block font-medium text-sm text-gray-700" for="email">Email</label>
          <input name="email" type="email" class="textbox mt-1 block w-full" v-model="form.email" required autofocus autocomplete="email" />
        </div>

        <div class="mt-4">
          <label class="block font-medium text-sm text-gray-700" for="password">Password</label>
          <input name="password" type="password" class="textbox mt-1 block w-full" v-model="form.password" required autocomplete="current-password" />
        </div>

        <div class="block mt-4">
          <label class="flex items-center">
            <input type="checkbox" name="remember" v-model="form.remember"
              class="rounded border-gray-300 text-indigo-600 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50" />
            <span class="ml-2 text-sm text-gray-600">Remember me</span>
          </label>
        </div>

        <div class="flex items-center justify-end mt-4">
          <button class="button ml-4" :class="{ 'opacity-25': form.processing }" :disabled="form.processing">
            Log in
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'LoginPage',
    data() {
      return {
        form: {
          email: '',
          password: '',
          remember: false,
        },
        error: this.$route.query.err,
      }
    }
  }
</script>
