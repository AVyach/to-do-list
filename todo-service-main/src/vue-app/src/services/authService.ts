import { AxiosInstance } from "axios";
import { LoginDTO, RegisterDTO, UserDTO } from "../dtos/authDTO";
import apiClient from "./apiClient";
class AuthService {
  private api: AxiosInstance;

  constructor() {
    this.api = apiClient;
  }

  async login(data: LoginDTO) {
    const response = await this.api.post("/auth/token", data);
    const token = response.data.access_token;
    const refresh_token = response.data.refresh_token;
    
    localStorage.setItem("access_token", token);
    localStorage.setItem("refresh_token", refresh_token)
    const userData = response.data.user;
    console.log(userData)
    const user: UserDTO = {
      ...userData,
      token: token,
    };
    localStorage.setItem("user", user.username)
    localStorage.setItem("user_id", user.id)
    return user;
  }

  async register(data: RegisterDTO): Promise<void> {
    await this.api.post("/auth/register", data);
  
  }

  logout(): void {
    localStorage.removeItem("user");
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_id");
    localStorage.removeItem("refresh_token");
    window.location.reload();
  }
}

export default new AuthService();
