export interface LoginDTO {
    username: string;
    password: string;
  }
  
  export interface RegisterDTO {
    username: string;
    email: string;
    password: string;
    confirmPassword: string;
  }
  
  export interface UserDTO {
    username: string;
    email: string;
    token: string;
    id: string;
  }