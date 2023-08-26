<script setup lang="ts">

import PageHeader from "~/components/page-header.vue";
import ToolBar from "~/components/tool-bar.vue";
</script>

<template>
<div class="page">
  <page-header/>
    <slot/>
  <tool-bar/>
</div>
</template>

<style scoped lang="sass">
@import "assets/colors"

.page
  height: 100vh
  width: 100vw
  background-color: $background-dark

</style>