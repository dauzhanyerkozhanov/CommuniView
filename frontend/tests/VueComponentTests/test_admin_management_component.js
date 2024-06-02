import { shallowMount } from '@vue/test-utils'
import axios from 'axios'
import AdminManagement from '@/vue_components/admin_management.vue'
jest.mock('axios')

describe('AdminManagement.vue', () => {
  let wrapper

  beforeEach(() => {
    wrapper = shallowMount(AdminManagement)
  })

  afterEach(() => {
    jest.clearAllMocks()
  })

  it('calls axios.get when "monitor" method is invoked', async () => {
    axios.get.mockResolvedValue({ data: {} })
    await wrapper.vm.monitor()
    expect(axios.get).toHaveBeenCalledWith('/admin/monitor')
  })

  it('calls axios.get when "accessDashboard" method is invoked', async () => {
    axios.get.mockResolvedValue({ data: {} })
    await wrapper.vm.accessDashboard()
    expect(axios.get).toHaveBeenCalledWith('/admin/dashboard')
  })

  it('calls axios.post when "executeTasks" method is invoked', async () => {
    axios.post.mockResolvedValue({ data: {} })
    await wrapper.vm.executeTasks()
    expect(axios.post).toHaveBeenCalledWith('/admin/execute')
  })

  it('calls axios.post when "logout" method is invoked', async () => {
    axios.post.mockResolvedValue({ data: {} })
    await wrapper.vm.logout()
    expect(axios.post).toHaveBeenCalledWith('/admin/logout')
  })

  it('handles errors when "monitor" method fails', async () => {
    const errorMessage = 'Network Error'
    axios.get.mockRejectedValue(new Error(errorMessage))
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {})

    await wrapper.vm.monitor()

    expect(consoleSpy).toHaveBeenCalledWith(new Error(errorMessage))
    consoleSpy.mockRestore()
  })

  it('handles errors when "accessDashboard" method fails', async () => {
    const errorMessage = 'Network Error'
    axios.get.mockRejectedValue(new Error(errorMessage))
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {})

    await wrapper.vm.accessDashboard()

    expect(consoleSpy).toHaveBeenCalledWith(new Error(errorMessage))
    consoleSpy.mockRestore()
  })

  it('handles errors when "executeTasks" method fails', async () => {
    const errorMessage = 'Network Error'
    axios.post.mockRejectedValue(new Error(errorMessage))
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {})

    await wrapper.vm.executeTasks()

    expect(consoleSpy).toHaveBeenCalledWith(new Error(errorMessage))
    consoleSpy.mockRestore()
  })

  it('handles errors when "logout" method fails', async () => {
    const errorMessage = 'Network Error'
    axios.post.mockRejectedValue(new Error(errorMessage))
    const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {})

    await wrapper.vm.logout()

    expect(consoleSpy).toHaveBeenCalledWith(new Error(errorMessage))
    consoleSpy.mockRestore()
  })
})
