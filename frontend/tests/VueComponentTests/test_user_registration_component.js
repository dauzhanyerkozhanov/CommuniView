import { shallowMount } from '@vue/test-utils';
import axios from 'axios';
import UserRegistration from '@/components/UserRegistration.vue';

jest.mock('axios');

describe('UserRegistration.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowMount(UserRegistration);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('registers a user', async () => {
    const registrationData = {
      username: 'testuser',
      email: 'testuser@example.com',
      password: 'testpassword'
    };
    axios.post.mockResolvedValueOnce({ data: {} });
    wrapper.setData(registrationData);
    await wrapper.vm.register();
    expect(axios.post).toHaveBeenCalledWith('/register_form', registrationData);
  });

  it('handles registration errors', async () => {
    const registrationData = {
      username: 'testuser',
      email: 'testuser@example.com',
      password: 'testpassword'
    };
    const errorResponse = { data: { errors: 'Registration error' } };
    axios.post.mockRejectedValueOnce(errorResponse);
    wrapper.setData(registrationData);
    await wrapper.vm.register();
    expect(wrapper.vm.errorMessage).toBe('Registration error');
  });

  it('renders error message when errorMessage is set', () => {
    wrapper.setData({ errorMessage: 'Registration error' });
    const errorMessage = wrapper.find('.error');
    expect(errorMessage.exists()).toBe(true);
    expect(errorMessage.text()).toBe('Registration error');
  });

  it('does not render error message when errorMessage is not set', () => {
    const errorMessage = wrapper.find('.error');
    expect(errorMessage.exists()).toBe(false);
  });

  it('clears error message after successful registration', async () => {
    wrapper.setData({ errorMessage: 'Registration error' });
    axios.post.mockResolvedValueOnce({ data: {} });
    await wrapper.vm.register();
    expect(wrapper.vm.errorMessage).toBe('');
  });

  it('handles network errors', async () => {
    const registrationData = {
      username: 'testuser',
      email: 'testuser@example.com',
      password: 'testpassword'
    };
    const networkError = new Error('Network Error');
    axios.post.mockRejectedValueOnce(networkError);
    wrapper.setData(registrationData);
    await wrapper.vm.register();
    expect(wrapper.vm.errorMessage).toBe('');
    expect(console.error).toHaveBeenCalledWith(networkError);
  });
});
