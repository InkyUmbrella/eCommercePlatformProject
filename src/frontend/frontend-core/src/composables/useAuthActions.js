import { ElMessageBox } from 'element-plus';

import { useUserStore } from '@/store/userStore';

export const useAuthActions = () => {
  const userStore = useUserStore();

  const logout = async () => {
    await ElMessageBox.confirm('确定要退出当前账号吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    });
    userStore.logout();
  };

  const switchAccount = async () => {
    await ElMessageBox.confirm('确定要退出当前账号并切换账号吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    });
    userStore.logout();
  };

  return {
    logout,
    switchAccount,
  };
};
