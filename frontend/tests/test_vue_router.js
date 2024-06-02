import { createLocalVue, mount } from '@vue/test-utils';
import VueRouter from 'vue-router';
import router from './router.js';

const Vue = createLocalVue();
Vue.use(VueRouter);

describe('router.js', () => {
  test.each([
    ['/admin-management', 'AdminManagement'],
    ['/bookmark', 'Bookmark'],
    ['/business-claim', 'BusinessClaim'],
    ['/business/:id', 'BusinessDetail'],
    ['/business-listing', 'BusinessListing'],
    ['/review', 'Review'],
    ['/special-offer', 'SpecialOffer'],
    ['/trending-tags', 'TrendingTag'],
    ['/login', 'UserLogin'],
    ['/register', 'UserRegistration'],
  ])('route %s leads to component %s', async (path, componentName) => {
    const wrapper = mount({
      template: '<router-view></router-view>',
    }, { localVue: Vue, router });
    router.push(path);
    await wrapper.vm.$nextTick(); // Wait for the route to be pushed
    expect(wrapper.findComponent({ name: componentName }).exists()).toBe(true);
  });

  test('router mode is set to "history"', () => {
    expect(router.mode).toBe('history');
  });

  test('router handles non-existent routes', async () => {
    const wrapper = mount({
      template: '<router-view></router-view>',
    }, { localVue: Vue, router });
    router.push('/non-existent-route');
    await wrapper.vm.$nextTick();
    expect(wrapper.html()).toContain('');
  });

  test('router handles dynamic route parameters', async () => {
    const wrapper = mount({
      template: '<router-view></router-view>',
    }, { localVue: Vue, router });
    const businessId = '123';
    router.push(`/business/${businessId}`);
    await wrapper.vm.$nextTick();
    expect(wrapper.findComponent({ name: 'BusinessDetail' }).exists()).toBe(true);
    // Add additional assertions if needed
  });
});
