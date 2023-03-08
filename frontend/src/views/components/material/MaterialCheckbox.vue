<template>
  <div class="form-check p-0">
    <input
        :id="id"
        class="form-check-input"
        type="checkbox"
        name="check"
        v-on:input="check"
    />
    <label :for="id" class="custom-control-label">
      <slot/>
    </label>
  </div>
</template>

<script>
export default {
  name: "MaterialCheckbox",
  props: {
    // name: {
    //   type: String,
    //   default: "",
    // },
    id: {
      type: String,
      default: "",
    },
    checked: Boolean,
  },
  methods: {
    check(e) {
      console.log(e)
      this.$emit("checked", document.getElementsByName('check')[0].checked);
    },
  }
};
</script>
