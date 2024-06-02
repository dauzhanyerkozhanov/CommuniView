import { shallowMount } from '@vue/test-utils';
import axios from 'axios';
import TrendingTag from '@/vue_components/trending_tag.vue';

jest.mock('axios');

describe('TrendingTag.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = shallowMount(TrendingTag);
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  it('fetches trending tags on component creation', () => {
    expect(axios.get).toHaveBeenCalledWith('/tags');
  });

  it('creates a new trending tag', async () => {
    const newTag = { id: '1', name: 'New Tag', popularityScore: 10 };
    axios.post.mockResolvedValue({ data: newTag });
    wrapper.setData({ tagForm: { name: 'New Tag', popularityScore: 10 } });
    await wrapper.vm.createTrendingTag();
    expect(axios.post).toHaveBeenCalledWith('/tags', wrapper.vm.tagForm);
    expect(wrapper.vm.tags).toContainEqual(newTag);
  });

  it('creates a new trending tag with invalid input', async () => {
    axios.post.mockRejectedValue(new Error('Invalid input'));
    wrapper.setData({ tagForm: { name: '', popularityScore: -1 } });
    await wrapper.vm.createTrendingTag();
    expect(axios.post).toHaveBeenCalledWith('/tags', wrapper.vm.tagForm);
    expect(console.error).toHaveBeenCalledWith(new Error('Invalid input'));
  });

  it('edits an existing trending tag', async () => {
    const updatedTag = { id: '1', name: 'Updated Tag', popularityScore: 20 };
    axios.put.mockResolvedValue({ data: updatedTag });
    wrapper.setData({ tags: [{ id: '1', name: 'Old Tag', popularityScore: 10 }] });
    wrapper.setData({ tagForm: { name: 'Updated Tag', popularityScore: 20 } });
    await wrapper.vm.editTrendingTag('1');
    expect(axios.put).toHaveBeenCalledWith('/tags/1', wrapper.vm.tagForm);
    expect(wrapper.vm.tags).toContainEqual(updatedTag);
  });

  it('deletes a trending tag', async () => {
    axios.delete.mockResolvedValue({});
    wrapper.setData({ tags: [{ id: '1', name: 'Tag 1' }, { id: '2', name: 'Tag 2' }] });
    await wrapper.vm.deleteTrendingTag('1');
    expect(axios.delete).toHaveBeenCalledWith('/tags/1');
    expect(wrapper.vm.tags).not.toContainEqual({ id: '1', name: 'Tag 1' });
    expect(wrapper.vm.tags).toContainEqual({ id: '2', name: 'Tag 2' });
  });

  it('fetches businesses for a tag', async () => {
    const businesses = [{ id: '1', name: 'Business 1' }, { id: '2', name: 'Business 2' }];
    axios.get.mockResolvedValue({ data: businesses });
    await wrapper.vm.getBusinessesForTag('1');
    expect(axios.get).toHaveBeenCalledWith('/tags/1/businesses');
    expect(wrapper.vm.businesses).toEqual(businesses);
  });
});
