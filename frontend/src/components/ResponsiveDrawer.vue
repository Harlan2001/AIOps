<script setup lang="ts">
defineOptions({ inheritAttrs: false })

withDefaults(defineProps<{
  open: boolean
  title?: string
  width?: number
}>(), {
  title: '',
  width: 760,
})

const emit = defineEmits<{
  'update:open': [value: boolean]
  close: []
}>()
</script>

<template>
  <a-drawer
    v-bind="$attrs"
    :open="open"
    :title="title"
    :width="`min(${width}px, 100vw)`"
    class="responsive-drawer"
    @update:open="emit('update:open', $event)"
    @close="emit('close')"
  >
    <template v-if="$slots.extra" #extra>
      <slot name="extra" />
    </template>
    <slot />
    <template v-if="$slots.footer" #footer>
      <slot name="footer" />
    </template>
  </a-drawer>
</template>
