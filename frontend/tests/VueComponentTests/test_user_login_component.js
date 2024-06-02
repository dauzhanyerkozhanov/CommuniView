import { shallowMount } from '@vue/test-utils';
import axios from 'axios';
import UserLogin from '@/components/UserLogin.vue';
jest.mock('axios');

describe('UserLogin.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowMount(UserLogin);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('logs in a user', async () => {
    const loginData = {
      username: 'testuser',
      password: 'testpassword'
    };
    axios.post.mockResolvedValueOnce();
    wrapper.setData(loginData);
    await wrapper.vm.login();
    expect(axios.post).toHaveBeenCalledWith('/login', loginData);
  });

  it('logs out a user', async () => {
    axios.get.mockResolvedValueOnce();
    await wrapper.vm.logout();
    expect(axios.get).toHaveBeenCalledWith('/logout');
  });

  it('renders the login form', () => {
    const form = wrapper.find('form');
    expect(form.exists()).toBe(true);
  });

  it('renders the username input field', () => {
    const usernameInput = wrapper.find('input[placeholder="Username"]');
    expect(usernameInput.exists()).toBe(true);
  });

  it('renders the password input field', () => {
    const passwordInput = wrapper.find('input[placeholder="Password"]');
    expect(passwordInput.exists()).toBe(true);
  });

  it('renders the login button', () => {
    const loginButton = wrapper.find('button[type="submit"]');
    expect(loginButton.exists()).toBe(true);
  });

  it('renders the logout button', () => {
    const logoutButton = wrapper.find('button:not([type="submit"])');
    expect(logoutButton.exists()).toBe(true);
  });

  it('updates username data on input', async () => {
    const usernameInput = wrapper.find('input[placeholder="Username"]');
    await usernameInput.setValue('newusername');
    expect(wrapper.vm.username).toBe('newusername');
  });

  it('updates password data on input', async () => {
    const passwordInput = wrapper.find('input[placeholder="Password"]');
    await passwordInput.setValue('newpassword');
    expect(wrapper.vm.password).toBe('newpassword');
  });

  it('handles login errors', async () => {
    const loginData = {
      username: 'testuser',
      password: 'testpassword'
    };
    const errorMessage = 'Login failed';
    axios.post.mockRejectedValueOnce(new Error(errorMessage));
    wrapper.setData(loginData);
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    await wrapper.vm.login();
    expect(consoleSpy).toHaveBeenCalledWith(new Error(errorMessage));
    consoleSpy.mockRestore();
  });

  it('handles logout errors', async () => {
    const errorMessage = 'Logout failed';
    axios.get.mockRejectedValueOnce(new Error(errorMessage));
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    await wrapper.vm.logout();
    expect(consoleSpy).toHaveBeenCalledWith(new Error(errorMessage));
    consoleSpy.mockRestore();
  });
});
