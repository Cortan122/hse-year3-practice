<template>
  <div class="pt-8 2xl:py-24">
    <div class="max-w-screen-xl mx-auto px-6 lg:px-8 xl:px-4 grid md:grid-cols-4 xl:grid-cols-5 gap-x-12 lg:gap-x-20">
      <div class="order-2 md:order-1 col-span-2 self-center mt-12 md:mt-0">
        <h1 class="text-gray-800 text-3xl md:text-4xl lg:text-5xl font-bold mb-2 md:mb-4 lg:mb-8">
          The
          <span class="text-red-500">SITE_NAME</span>
          Project Tracker
        </h1>
        <p class="text-lg xl:text-xl text-gray-600 mb-6 lg:mb-8 xl:mb-10">
          &mdash; это веб приложение для отслеживания работы над вашими проектами.
          Вы можете организовывать проекты по компаниям и по клиентам, и выполнять задачи на время.
          Мы следим за временем и гарантируем что над каждой задачей может одновременно работать только один человек.
          Потом можно будет посмотреть статистику выполненной работы.
        </p>

        <div class="flex space-x-4 mb-6 mx-10">
          <button class="focus:outline-none inline-block bg-gradient-to-br from-red-600 to-red-700 hover:from-red-500 hover:to-red-700 font-semibold rounded-lg py-2 px-5 text-white">
            <router-link to="/login">Get Started</router-link>
          </button>
          <button class="focus:outline-none inline-block bg-gradient-to-br from-emerald-600 to-emerald-700 hover:from-emerald-500 hover:to-emerald-700 font-semibold rounded-lg py-2 px-5 text-white">
            <a href="https://github.com/Cortan122/hse-year3-practice" target="_blank">Source Code</a>
          </button>
        </div>
      </div>

      <div class="order-1 md:order-2 col-span-2 xl:col-span-3">
        <img src='@/assets/undraw_scrum_board.svg' class="rounded-lg" alt="scrum board">
      </div>
    </div>
  </div>

</template>
