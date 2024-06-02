import { shallowMount } from '@vue/test-utils';
import axios from 'axios';
import Bookmark from '@/components/Bookmark.vue';

jest.mock('axios');

describe('Bookmark.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowMount(Bookmark);
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  it('fetches bookmarks on component creation', () => {
    expect(axios.get).toHaveBeenCalledWith('/bookmark');
  });

  it('creates a new bookmark', async () => {
    const newBookmarkData = {
      associated_user: 'User Name',
      associated_business: 'Business Name'
    };
    axios.post.mockResolvedValueOnce();
    await wrapper.vm.createBookmark();
    expect(axios.post).toHaveBeenCalledWith('/bookmark', newBookmarkData);
  });

  it('creates a new bookmark with invalid data', async () => {
    const invalidBookmarkData = {
      associated_user: '',
      associated_business: ''
    };
    axios.post.mockRejectedValueOnce(new Error('Invalid data'));
    await wrapper.vm.createBookmark();
    expect(axios.post).toHaveBeenCalledWith('/bookmark', invalidBookmarkData);
    expect(wrapper.vm.errorMessage).toBe('Failed to create bookmark.');
  });

  it('edits a bookmark', async () => {
    const updatedBookmarkData = {
      new_associated_user: 'Updated User Name',
      new_associated_business: 'Updated Business Name'
    };
    axios.put.mockResolvedValueOnce();
    await wrapper.vm.editBookmark(1);
    expect(axios.put).toHaveBeenCalledWith('/bookmark/1/edit', updatedBookmarkData);
  });

  it('edits a bookmark with invalid data', async () => {
    const invalidBookmarkData = {
      new_associated_user: '',
      new_associated_business: ''
    };
    axios.put.mockRejectedValueOnce(new Error('Invalid data'));
    await wrapper.vm.editBookmark(1);
    expect(axios.put).toHaveBeenCalledWith('/bookmark/1/edit', invalidBookmarkData);
    expect(wrapper.vm.errorMessage).toBe('Failed to edit bookmark.');
  });

  it('deletes a bookmark', async () => {
    axios.delete.mockResolvedValueOnce();
    await wrapper.vm.deleteBookmark(1);
    expect(axios.delete).toHaveBeenCalledWith('/bookmark/1');
  });

  it('handles error when deleting a bookmark', async () => {
    axios.delete.mockRejectedValueOnce(new Error('Failed to delete'));
    await wrapper.vm.deleteBookmark(1);
    expect(axios.delete).toHaveBeenCalledWith('/bookmark/1');
    expect(wrapper.vm.errorMessage).toBe('Failed to delete bookmark.');
  });
});
